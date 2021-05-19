from Function.api_function import *
import allure
import datetime
from decimal import *


# convert order相关cases
class TestConvertOrderApi:

    @allure.testcase('test_convert_order_001 根据id编号查询单笔交易')
    def test_convert_order_001(self):
        time_list = get_zero_time(day_time='2021-05-19')
        cfx_info = []
        for i in time_list:
            info = sqlFunction().get_cfx_detail(end_time=i)
            if info is not None:
                 cfx_info.append(info)
        print(cfx_info)
        # cfx_info = [{'id': 209, 'deal_no': '2dde1c96-050a-4410-8ba3-e73882657e27', 'counterparty': 'fa546596-39ae-4b79-bb75-196e2dc6e6cf', 'created_at': datetime.datetime(2021, 5, 18, 2, 54, 41), 'transaction_time': datetime.datetime(2021, 5, 18, 2, 54, 42), 'trading_amount': '50', 'pnl_amount': '169567.762499', 'rate': '0.000294867369026', 'trading_direction': 1, 'pnl_direction': 2, 'maturity_date': '', 'source_type': 1, 'book_id': 3, 'aggregation_no': 1621306500, 'gnl': '169692.4852566315487', 'cost': ''}, {'id': 210, 'deal_no': '9901f16a-ff32-4191-b650-7d5aad20f915', 'counterparty': 'fa546596-39ae-4b79-bb75-196e2dc6e6cf', 'created_at': datetime.datetime(2021, 5, 18, 2, 58, 5), 'transaction_time': datetime.datetime(2021, 5, 18, 2, 58, 6), 'trading_amount': '50', 'pnl_amount': '170602.9325', 'rate': '3412.05865', 'trading_direction': 2, 'pnl_direction': 1, 'maturity_date': '', 'source_type': 1, 'book_id': 3, 'aggregation_no': 1621306740, 'gnl': '115.4325', 'cost': ''}, {'id': 211, 'deal_no': 'cef85fa4-4ada-4f45-944d-c2ba06fab58f', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 18, 6, 3, 32), 'transaction_time': datetime.datetime(2021, 5, 18, 6, 3, 33), 'trading_amount': '0.01084172', 'pnl_amount': '0.13987526', 'rate': '12.90157549', 'trading_direction': 2, 'pnl_direction': 1, 'maturity_date': '', 'source_type': 1, 'book_id': 2, 'aggregation_no': 1621317840, 'gnl': '0.0001392905155408', 'cost': ''}, {'id': 213, 'deal_no': '859b705d-a865-467c-ab7f-7dd5c35c1803', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 18, 6, 18, 35), 'transaction_time': datetime.datetime(2021, 5, 18, 6, 18, 36), 'trading_amount': '0.11482462', 'pnl_amount': '1.47295532', 'rate': '12.82787026', 'trading_direction': 2, 'pnl_direction': 1, 'maturity_date': '', 'source_type': 1, 'book_id': 2, 'aggregation_no': 1621318740, 'gnl': '0.00146694193281', 'cost': ''}, {'id': 215, 'deal_no': 'bad67144-8baf-4132-81f7-3d4091f3852b', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 18, 6, 19, 2), 'transaction_time': datetime.datetime(2021, 5, 18, 6, 19, 3), 'trading_amount': '0.0024768', 'pnl_amount': '0.03175058', 'rate': '12.81915154', 'trading_direction': 2, 'pnl_direction': 1, 'maturity_date': '', 'source_type': 1, 'book_id': 2, 'aggregation_no': 1621318800, 'gnl': '0.00003162118176', 'cost': ''}, {'id': 216, 'deal_no': '58ec2816-c81c-44bc-8c24-a98ee7d8c386', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 18, 6, 21, 16), 'transaction_time': datetime.datetime(2021, 5, 18, 6, 21, 16), 'trading_amount': '0.07073112', 'pnl_amount': '0.90555354', 'rate': '12.80275994', 'trading_direction': 2, 'pnl_direction': 1, 'maturity_date': '', 'source_type': 1, 'book_id': 2, 'aggregation_no': 1621318920, 'gnl': '-0.0001552802716032', 'cost': ''}, {'id': 219, 'deal_no': '79e72be3-f80c-4592-818f-b0e5b88ef201', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 18, 6, 28, 31), 'transaction_time': datetime.datetime(2021, 5, 18, 6, 28, 31), 'trading_amount': '0.07029341', 'pnl_amount': '0.90225057', 'rate': '12.83549311', 'trading_direction': 2, 'pnl_direction': 1, 'maturity_date': '', 'source_type': 1, 'book_id': 2, 'aggregation_no': 1621319340, 'gnl': '0.0008985522248208', 'cost': ''}, {'id': 222, 'deal_no': '06050140-b8af-4e3d-9e76-ccd9c86b14ad', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 18, 6, 29, 9), 'transaction_time': datetime.datetime(2021, 5, 18, 6, 29, 10), 'trading_amount': '0.07101921', 'pnl_amount': '0.91078538', 'rate': '0.0779757899145577', 'trading_direction': 1, 'pnl_direction': 2, 'maturity_date': '', 'source_type': 1, 'book_id': 2, 'aggregation_no': 1621319400, 'gnl': '0.906156462924912844646583', 'cost': ''}, {'id': 224, 'deal_no': 'b058841e-7230-4227-a189-63a50cfec6bb', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 18, 6, 31), 'transaction_time': datetime.datetime(2021, 5, 18, 6, 31), 'trading_amount': '0.1642838', 'pnl_amount': '2.11106946', 'rate': '12.85013776', 'trading_direction': 2, 'pnl_direction': 1, 'maturity_date': '', 'source_type': 1, 'book_id': 2, 'aggregation_no': 1621319520, 'gnl': '0.002102387430902', 'cost': ''}, {'id': 229, 'deal_no': '6b9e4677-10b5-4350-8028-2ce897c0421f', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 18, 6, 32, 3), 'transaction_time': datetime.datetime(2021, 5, 18, 6, 32, 3), 'trading_amount': '0.00057898', 'pnl_amount': '26.187122', 'rate': '0.0000221095981403', 'trading_direction': 1, 'pnl_direction': 2, 'maturity_date': '', 'source_type': 1, 'book_id': 1, 'aggregation_no': 1621319580, 'gnl': '26.288876377198984868729106', 'cost': ''}, {'id': 232, 'deal_no': '8a0f952f-13fb-4df9-a760-049122c0c715', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 18, 6, 34), 'transaction_time': datetime.datetime(2021, 5, 18, 6, 34), 'trading_amount': '0.07458068', 'pnl_amount': '0.95710001', 'rate': '12.83308239', 'trading_direction': 2, 'pnl_direction': 1, 'maturity_date': '', 'source_type': 1, 'book_id': 2, 'aggregation_no': 1621319700, 'gnl': '0.000953163464604', 'cost': ''}, {'id': 235, 'deal_no': '2bc74f1d-9ac3-4923-a46e-6597e14af366', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 18, 7, 35, 29), 'transaction_time': datetime.datetime(2021, 5, 18, 7, 35, 29), 'trading_amount': '0.01', 'pnl_amount': '451.746295', 'rate': '45174.6295', 'trading_direction': 2, 'pnl_direction': 1, 'maturity_date': '', 'source_type': 1, 'book_id': 1, 'aggregation_no': 1621323360, 'gnl': '0.451295', 'cost': ''}, {'id': 236, 'deal_no': 'ba35955b-5cd6-4813-ab80-46a4df6fe364', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 18, 7, 39, 31), 'transaction_time': datetime.datetime(2021, 5, 18, 7, 39, 31), 'trading_amount': '0.17927988', 'pnl_amount': '2.30733934', 'rate': '12.87004067', 'trading_direction': 2, 'pnl_direction': 1, 'maturity_date': '', 'source_type': 1, 'book_id': 2, 'aggregation_no': 1621323600, 'gnl': '0.002297749546014', 'cost': ''}, {'id': 239, 'deal_no': 'a4dd3d23-4b10-4f6b-b7e7-3642e00f2ac4', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 18, 7, 40, 7), 'transaction_time': datetime.datetime(2021, 5, 18, 7, 40, 7), 'trading_amount': '0.04962953', 'pnl_amount': '0.63775025', 'rate': '0.0778196945521114', 'trading_direction': 1, 'pnl_direction': 2, 'maturity_date': '', 'source_type': 1, 'book_id': 2, 'aggregation_no': 1621323660, 'gnl': '0.634524465772519750710358', 'cost': ''}, {'id': 244, 'deal_no': 'f38e6346-14aa-40d6-a19c-2fe5f46a58b7', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 18, 7, 41, 55), 'transaction_time': datetime.datetime(2021, 5, 18, 7, 41, 55), 'trading_amount': '0.11353387', 'pnl_amount': '398.106855', 'rate': '3506.503', 'trading_direction': 2, 'pnl_direction': 1, 'maturity_date': '', 'source_type': 1, 'book_id': 3, 'aggregation_no': 1621323720, 'gnl': '0.39770914661', 'cost': ''}, {'id': 245, 'deal_no': '18fed08f-2d87-4cd9-9d22-91dac97b15a0', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 18, 7, 42, 7), 'transaction_time': datetime.datetime(2021, 5, 18, 7, 42, 7), 'trading_amount': '0.00541115', 'pnl_amount': '18.934696', 'rate': '0.0002857798272764', 'trading_direction': 1, 'pnl_direction': 2, 'maturity_date': '', 'source_type': 1, 'book_id': 3, 'aggregation_no': 1621323780, 'gnl': '18.95498634610248763330814', 'cost': ''}, {'id': 248, 'deal_no': '926735a2-7cba-43f5-81e1-92368d123bd1', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 18, 7, 45, 15), 'transaction_time': datetime.datetime(2021, 5, 18, 7, 45, 16), 'trading_amount': '0.03488437', 'pnl_amount': '0.45032587', 'rate': '12.90910156', 'trading_direction': 2, 'pnl_direction': 1, 'maturity_date': '', 'source_type': 1, 'book_id': 2, 'aggregation_no': 1621323960, 'gnl': '0.0004484305529449', 'cost': ''}, {'id': 253, 'deal_no': '020781f2-88f6-4758-a6df-a8343843d0dc', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 18, 7, 46, 1), 'transaction_time': datetime.datetime(2021, 5, 18, 7, 46, 2), 'trading_amount': '0.00064442', 'pnl_amount': '29.00157', 'rate': '0.0000222205179085', 'trading_direction': 1, 'pnl_direction': 2, 'maturity_date': '', 'source_type': 1, 'book_id': 1, 'aggregation_no': 1621324020, 'gnl': '29.03015435568065384940443', 'cost': ''}, {'id': 256, 'deal_no': '1c223cec-4eb6-4062-b101-25a6188c25be', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 18, 7, 47, 6), 'transaction_time': datetime.datetime(2021, 5, 18, 7, 47, 7), 'trading_amount': '0.01998463', 'pnl_amount': '69.551043', 'rate': '3480.22675', 'trading_direction': 2, 'pnl_direction': 1, 'maturity_date': '', 'source_type': 1, 'book_id': 3, 'aggregation_no': 1621324080, 'gnl': '0.0854692663525', 'cost': ''}, {'id': 260, 'deal_no': '8b44b366-3f5d-4f9c-9f7b-3d1e655e6a70', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 18, 8, 14, 51), 'transaction_time': datetime.datetime(2021, 5, 18, 8, 14, 51), 'trading_amount': '0.16301117', 'pnl_amount': '2.09734753', 'rate': '12.86628112', 'trading_direction': 2, 'pnl_direction': 1, 'maturity_date': '', 'source_type': 1, 'book_id': 2, 'aggregation_no': 1621325700, 'gnl': '-0.0000577450768608', 'cost': ''}, {'id': 261, 'deal_no': 'ddfa1861-239d-43d0-b10f-a964a018ed04', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 18, 8, 15, 1), 'transaction_time': datetime.datetime(2021, 5, 18, 8, 15, 1), 'trading_amount': '0.00285682', 'pnl_amount': '0.03668342', 'rate': '0.0778778912000644', 'trading_direction': 1, 'pnl_direction': 2, 'maturity_date': '', 'source_type': 1, 'book_id': 2, 'aggregation_no': 1621325760, 'gnl': '0.036497562020258632020792', 'cost': ''}, {'id': 267, 'deal_no': '39b867fa-633b-481f-ad09-88eebd3922d2', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 18, 8, 16, 1), 'transaction_time': datetime.datetime(2021, 5, 18, 8, 16, 2), 'trading_amount': '0.02933212', 'pnl_amount': '1325.511609', 'rate': '0.0000221289046314', 'trading_direction': 1, 'pnl_direction': 2, 'maturity_date': '', 'source_type': 1, 'book_id': 1, 'aggregation_no': 1621325820, 'gnl': '1326.838447', 'cost': '45235'}, {'id': 269, 'deal_no': '09036028-fe80-4642-ad7b-4ae2274f8c4d', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 18, 8, 17, 1), 'transaction_time': datetime.datetime(2021, 5, 18, 8, 17, 2), 'trading_amount': '0.00701914', 'pnl_amount': '24.618877', 'rate': '0.0002851123646361', 'trading_direction': 1, 'pnl_direction': 2, 'maturity_date': '', 'source_type': 1, 'book_id': 3, 'aggregation_no': 1621325880, 'gnl': '24.643496', 'cost': '3510.9'}, {'id': 272, 'deal_no': '2b268c26-e1a3-46b9-b737-4b904b9d9772', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 18, 8, 19, 43), 'transaction_time': datetime.datetime(2021, 5, 18, 8, 19, 44), 'trading_amount': '0.18514686', 'pnl_amount': '2.38347153', 'rate': '12.87341051', 'trading_direction': 2, 'pnl_direction': 1, 'maturity_date': '', 'source_type': 1, 'book_id': 2, 'aggregation_no': 1621326000, 'gnl': '0.00238109', 'cost': '12.86054996'}, {'id': 274, 'deal_no': '8dd708d8-2a00-4fec-9a4d-22f5ebebdd74', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 18, 8, 20, 5), 'transaction_time': datetime.datetime(2021, 5, 18, 8, 20, 5), 'trading_amount': '0.00264218', 'pnl_amount': '0.03403072', 'rate': '12.87977031', 'trading_direction': 2, 'pnl_direction': 1, 'maturity_date': '', 'source_type': 1, 'book_id': 2, 'aggregation_no': 1621326060, 'gnl': '0.00003399', 'cost': '12.8669034'}, {'id': 280, 'deal_no': 'a01950c2-36fa-4a71-b3be-1cae19564981', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 18, 8, 21, 56), 'transaction_time': datetime.datetime(2021, 5, 18, 8, 21, 57), 'trading_amount': '0.05996862', 'pnl_amount': '211.36066', 'rate': '3524.521', 'trading_direction': 2, 'pnl_direction': 1, 'maturity_date': '', 'source_type': 1, 'book_id': 3, 'aggregation_no': 1621326120, 'gnl': '0.211149', 'cost': '3521'}, {'id': 281, 'deal_no': '75b8ff3b-d165-46fa-bfaf-9610386a9d3f', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 18, 8, 22, 7), 'transaction_time': datetime.datetime(2021, 5, 18, 8, 22, 8), 'trading_amount': '0.00923965', 'pnl_amount': '32.499827', 'rate': '0.0002842985560718', 'trading_direction': 1, 'pnl_direction': 2, 'maturity_date': '', 'source_type': 1, 'book_id': 3, 'aggregation_no': 1621326180, 'gnl': '32.532343', 'cost': '3520.95'}, {'id': 284, 'deal_no': '25ecfb8c-b1fe-4a16-9588-8daab285bfe1', 'counterparty': '5b879a4e-b96a-4e82-9094-f4e7edf96fc0', 'created_at': datetime.datetime(2021, 5, 18, 8, 37, 33), 'transaction_time': datetime.datetime(2021, 5, 18, 8, 37, 33), 'trading_amount': '0.01', 'pnl_amount': '451.842705', 'rate': '0.0000221315955516', 'trading_direction': 1, 'pnl_direction': 2, 'maturity_date': '', 'source_type': 1, 'book_id': 1, 'aggregation_no': 1621327080, 'gnl': '452.294999', 'cost': '45229.5'}, {'id': 285, 'deal_no': 'f62b02d7-b989-481e-abde-a5d53ed9c0b9', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 18, 8, 51, 35), 'transaction_time': datetime.datetime(2021, 5, 18, 8, 51, 35), 'trading_amount': '0.005', 'pnl_amount': '0.06437953', 'rate': '0.0776644280379393', 'trading_direction': 1, 'pnl_direction': 2, 'maturity_date': '', 'source_type': 1, 'book_id': 2, 'aggregation_no': 1621327920, 'gnl': '0.06405565', 'cost': '12.8887964'}, {'id': 286, 'deal_no': '005a122a-767d-428a-b01a-89343184f9bd', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 18, 8, 53, 6), 'transaction_time': datetime.datetime(2021, 5, 18, 8, 53, 6), 'trading_amount': '0.06605213', 'pnl_amount': '0.85194288', 'rate': '12.89803801', 'trading_direction': 2, 'pnl_direction': 1, 'maturity_date': '', 'source_type': 1, 'book_id': 2, 'aggregation_no': 1621328040, 'gnl': '0.00085109', 'cost': '12.88515285'}, {'id': 293, 'deal_no': '79d1ef75-79de-4a03-84d1-5c2f5299313d', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 18, 8, 54, 5), 'transaction_time': datetime.datetime(2021, 5, 18, 8, 54, 5), 'trading_amount': '0.08166334', 'pnl_amount': '3672.521547', 'rate': '0.000022236313374', 'trading_direction': 1, 'pnl_direction': 2, 'maturity_date': '', 'source_type': 1, 'book_id': 1, 'aggregation_no': 1621328100, 'gnl': '3676.197743', 'cost': '45016.5'}, {'id': 296, 'deal_no': '6ba4d02c-a6f5-4f11-8120-01876c7b63c5', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 18, 8, 55, 4), 'transaction_time': datetime.datetime(2021, 5, 18, 8, 55, 4), 'trading_amount': '0.00609923', 'pnl_amount': '21.332043', 'rate': '3497.494', 'trading_direction': 2, 'pnl_direction': 1, 'maturity_date': '', 'source_type': 1, 'book_id': 3, 'aggregation_no': 1621328160, 'gnl': '0.02131', 'cost': '3494'}, {'id': 298, 'deal_no': '15290d89-5833-4108-8458-d9513334c3b3', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 18, 9, 21, 29), 'transaction_time': datetime.datetime(2021, 5, 18, 9, 21, 29), 'trading_amount': '0.12948317', 'pnl_amount': '1.67931789', 'rate': '12.96939127', 'trading_direction': 2, 'pnl_direction': 1, 'maturity_date': '', 'source_type': 1, 'book_id': 2, 'aggregation_no': 1621329720, 'gnl': '0.00167763', 'cost': '12.95643484'}, {'id': 301, 'deal_no': '12f7551b-62f7-4132-ba51-4a125d6e400f', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 18, 9, 22, 1), 'transaction_time': datetime.datetime(2021, 5, 18, 9, 22, 1), 'trading_amount': '0.05299635', 'pnl_amount': '0.68595937', 'rate': '0.0772587293745982', 'trading_direction': 1, 'pnl_direction': 2, 'maturity_date': '', 'source_type': 1, 'book_id': 2, 'aggregation_no': 1621329780, 'gnl': '0.68255159', 'cost': '12.95647765'}, {'id': 305, 'deal_no': '6623092e-51dc-4e3e-a116-7368097802f6', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 18, 9, 27, 8), 'transaction_time': datetime.datetime(2021, 5, 18, 9, 27, 8), 'trading_amount': '0.01268756', 'pnl_amount': '0.16457306', 'rate': '12.97121466', 'trading_direction': 2, 'pnl_direction': 1, 'maturity_date': '', 'source_type': 1, 'book_id': 2, 'aggregation_no': 1621330080, 'gnl': '0.0001644', 'cost': '12.9582564'}, {'id': 311, 'deal_no': '1ec5d133-4d06-44a4-a352-22c4a887af7b', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 18, 9, 28, 9), 'transaction_time': datetime.datetime(2021, 5, 18, 9, 28, 10), 'trading_amount': '0.00058953', 'pnl_amount': '26.475165', 'rate': '44908.3635', 'trading_direction': 2, 'pnl_direction': 1, 'maturity_date': '', 'source_type': 1, 'book_id': 1, 'aggregation_no': 1621330140, 'gnl': '-0.00686', 'cost': '44920'}, {'id': 313, 'deal_no': 'd4c6537a-5d4e-43e8-b50c-dca716879c02', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 18, 9, 29, 10), 'transaction_time': datetime.datetime(2021, 5, 18, 9, 29, 11), 'trading_amount': '0.03032468', 'pnl_amount': '104.997961', 'rate': '3462.459', 'trading_direction': 2, 'pnl_direction': 1, 'maturity_date': '', 'source_type': 1, 'book_id': 3, 'aggregation_no': 1621330200, 'gnl': '0.104893', 'cost': '3459'}, {'id': 317, 'deal_no': 'bf454fb1-23ad-4ed5-9730-9c5e5300e52e', 'counterparty': '0f9e2184-2708-4a81-8aff-44f25781968e', 'created_at': datetime.datetime(2021, 5, 18, 9, 36, 13), 'transaction_time': datetime.datetime(2021, 5, 18, 9, 36, 13), 'trading_amount': '0.005', 'pnl_amount': '0.06462906', 'rate': '0.0773645749497453', 'trading_direction': 1, 'pnl_direction': 2, 'maturity_date': '', 'source_type': 1, 'book_id': 2, 'aggregation_no': 1621330620, 'gnl': '0.06430693', 'cost': '12.93875138'}, {'id': 318, 'deal_no': '9e0fe52e-409d-4974-ad15-e35977bba292', 'counterparty': '5b879a4e-b96a-4e82-9094-f4e7edf96fc0', 'created_at': datetime.datetime(2021, 5, 18, 10, 31, 4), 'transaction_time': datetime.datetime(2021, 5, 18, 10, 31, 4), 'trading_amount': '0.01', 'pnl_amount': '451.2483', 'rate': '0.0000221607483064', 'trading_direction': 1, 'pnl_direction': 2, 'maturity_date': '', 'source_type': 1, 'book_id': 1, 'aggregation_no': 1621333920, 'gnl': '451.699999', 'cost': '45170'}, {'id': 319, 'deal_no': 'c7857e39-f74f-4821-9f2a-5f3c8b8a3abb', 'counterparty': '5b879a4e-b96a-4e82-9094-f4e7edf96fc0', 'created_at': datetime.datetime(2021, 5, 18, 10, 34, 3), 'transaction_time': datetime.datetime(2021, 5, 18, 10, 34, 3), 'trading_amount': '0.01', 'pnl_amount': '0.12901272', 'rate': '0.0775117368271904', 'trading_direction': 1, 'pnl_direction': 2, 'maturity_date': '', 'source_type': 1, 'book_id': 2, 'aggregation_no': 1621334100, 'gnl': '0.12836674', 'cost': '12.91418618'}, {'id': 320, 'deal_no': '35899d77-c321-4c57-bb00-71f78a6ba5e7', 'counterparty': '5b879a4e-b96a-4e82-9094-f4e7edf96fc0', 'created_at': datetime.datetime(2021, 5, 18, 10, 36, 12), 'transaction_time': datetime.datetime(2021, 5, 18, 10, 36, 13), 'trading_amount': '0.005', 'pnl_amount': '0.06454447', 'rate': '0.0774659658604777', 'trading_direction': 1, 'pnl_direction': 2, 'maturity_date': '', 'source_type': 1, 'book_id': 2, 'aggregation_no': 1621334220, 'gnl': '0.06422175', 'cost': '12.92181657'}, {'id': 321, 'deal_no': '78f39371-93f6-473f-8672-8fe67ea4fa1c', 'counterparty': '5b879a4e-b96a-4e82-9094-f4e7edf96fc0', 'created_at': datetime.datetime(2021, 5, 18, 10, 51, 34), 'transaction_time': datetime.datetime(2021, 5, 18, 10, 51, 35), 'trading_amount': '0.01', 'pnl_amount': '0.1292054', 'rate': '0.0773961406502696', 'trading_direction': 1, 'pnl_direction': 2, 'maturity_date': '', 'source_type': 1, 'book_id': 2, 'aggregation_no': 1621335120, 'gnl': '0.12856078', 'cost': '12.93347437'}, {'id': 323, 'deal_no': '644837a1-c619-41fd-b292-f635d2c68ba0', 'counterparty': '5b879a4e-b96a-4e82-9094-f4e7edf96fc0', 'created_at': datetime.datetime(2021, 5, 18, 10, 55, 53), 'transaction_time': datetime.datetime(2021, 5, 18, 10, 55, 53), 'trading_amount': '0.02', 'pnl_amount': '0.25837774', 'rate': '0.0774060470113257', 'trading_direction': 1, 'pnl_direction': 2, 'maturity_date': '', 'source_type': 1, 'book_id': 2, 'aggregation_no': 1621335360, 'gnl': '0.25708826', 'cost': '12.93181915'}, {'id': 324, 'deal_no': 'b5ce9d9b-5d16-4327-95f7-5bc27a6ad154', 'counterparty': '5b879a4e-b96a-4e82-9094-f4e7edf96fc0', 'created_at': datetime.datetime(2021, 5, 18, 11, 12, 58), 'transaction_time': datetime.datetime(2021, 5, 18, 11, 12, 59), 'trading_amount': '0.01', 'pnl_amount': '0.1290457', 'rate': '0.0774919271583758', 'trading_direction': 1, 'pnl_direction': 2, 'maturity_date': '', 'source_type': 1, 'book_id': 2, 'aggregation_no': 1621336380, 'gnl': '0.12839995', 'cost': '12.9174875'}, {'id': 325, 'deal_no': '48c27426-f1e3-40de-aacd-a64b58881a28', 'counterparty': '5b879a4e-b96a-4e82-9094-f4e7edf96fc0', 'created_at': datetime.datetime(2021, 5, 18, 11, 13, 16), 'transaction_time': datetime.datetime(2021, 5, 18, 11, 13, 16), 'trading_amount': '0.01', 'pnl_amount': '0.12924623', 'rate': '12.92462393', 'trading_direction': 2, 'pnl_direction': 1, 'maturity_date': '', 'source_type': 1, 'book_id': 2, 'aggregation_no': 1621336440, 'gnl': '0.00012911', 'cost': '12.91171222'}]
        # cfx_list = []
        # for y in cfx_info:
        #     cfx_dict = {}
        #     if y['book_id'] == 1:
        #         if y['trading_direction'] == 1:
        #             print(1)
        #         elif y['trading_direction'] == 2:
        #             print(2)
        #         print(y)
        #     elif y['book_id'] == 2:
        #         if y['trading_direction'] == 1:
        #             print(1)
        #         elif y['trading_direction'] == 2:
        #             print(2)
        #     elif y['book_id'] == 3:
        #         print(y)
        #     cfx_list.append(cfx_dict)