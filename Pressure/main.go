package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"sync"
	"syscall"
	"time"
	"github.com/myzhan/boomer"
)

func foo() {
	start := time.Now()
	seedUrl := "https://api.latibac.com/api/v1/core/account"
	resp, err := http.Get(seedUrl)

	if err != nil {
		log.Println(err)
		return
	}

	defer resp.Body.Close()
	fmt.Println(resp.Status)
	elapsed := time.Since(start)
	if resp.Status == "200 OK" {
		boomer.RecordSuccess("http", "sostreq", elapsed.Nanoseconds()/int64(time.Millisecond), int64(10))
	} else {
		boomer.RecordFailure("http", "sostreq", elapsed.Nanoseconds()/int64(time.Millisecond), "sostreq not equal")
	}
}

func bar() {
	start := time.Now()
	time.Sleep(100 * time.Millisecond)
	elapsed := time.Since(start)

	// Report your test result as a failure, if you write it in python, it will looks like this
	// events.request_failure.fire(request_type="udp", name="bar", response_time=100, exception=Exception("udp error"))
	globalBoomer.RecordFailure("udp", "bar", elapsed.Nanoseconds()/int64(time.Millisecond), "udp error")
}

func waitForQuit() {
	wg := sync.WaitGroup{}
	wg.Add(1)

	quitByMe := false
	go func() {
		c := make(chan os.Signal)
		signal.Notify(c, syscall.SIGINT, syscall.SIGTERM)
		<-c
		quitByMe = true
		globalBoomer.Quit()
		wg.Done()
	}()

	boomer.Events.Subscribe("boomer:quit", func() {
		if !quitByMe {
			wg.Done()
		}
	})

	wg.Wait()
}

var globalBoomer = boomer.NewBoomer("127.0.0.1", 5557)

func main() {
	log.SetFlags(log.LstdFlags | log.Lshortfile)

	task1 := &boomer.Task{
		Name:   "foo",
		Weight: 1,
		Fn:     foo,
	}

	task2 := &boomer.Task{
		Name:   "bar",
		Weight: 0,
		Fn:     bar,
	}

	globalBoomer.Run(task1, task2)

	waitForQuit()
	log.Println("shut down")
}
