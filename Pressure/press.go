package main

import "time"
import "github.com/myzhan/boomer"

func foo(){
	start := time.Now()
	time.Sleep(100 * time.Millisecond)
	elapsed := time.Since(start)

	/*
	   Report your test result as a success
	*/
	boomer.RecordSuccess("http", "foo", elapsed.Nanoseconds()/int64(time.Millisecond), int64(10))
}

func bar(){
	start := time.Now()
	time.Sleep(100 * time.Millisecond)
	elapsed := time.Since(start)

	/*
	   Report your test result as a failure
	*/
	boomer.RecordFailure("udp", "bar", elapsed.Nanoseconds()/int64(time.Millisecond), "udp error")
}

func main(){
	task1 := &boomer.Task{
		Name: "foo",
		// The weight is used to distribute goroutines over multiple tasks.
		Weight: 10,
		Fn: foo,
	}

	task2 := &boomer.Task{
		Name: "bar",
		Weight: 20,
		Fn: bar,
	}

	boomer.Run(task1, task2)
}
