import unittest, json
from server import classify



class TestResponses(unittest.TestCase):
    def test(self):
        with open('tests/test.json', 'r', encoding='utf-8') as json_data:
            tests = json.load(json_data)
        test_list = []
        for test_case in tests['tests']:
            right_tag = test_case['right_tag']
            questions = test_case['questions']
            for question in questions:
                predicted_tag = classify(question)
                print(f":_:_:_:_:_:_:_: {predicted_tag} :_:_:_:_:_:")
                if not predicted_tag:
                    predicted_tag = 'no_response'
                else:
                    number = float(predicted_tag[0][1])
                    if  number > 0.7:
                        test = { "question": question,
                                "right_tag": right_tag,
                                "predicted_tag": predicted_tag[0][0]
                                }
                    else:
                        test = { "question": question,
                                "right_tag": right_tag,
                                "predicted_tag": "no_response"
                                }
                    test_list.append(test)
        test_file = { "results": test_list }
        print(test_file)
        with open('tests/results.json', 'w', encoding='utf-8') as json_result:
            json.dump(test_file,json_result,indent=2)

        with open('tests/results.json', 'r', encoding='utf-8') as json_test_results:
            test_results = json.load(json_test_results)
        total = 0
        test_ok = 0
        for test_case in test_results['results']:
            total += 1
            if test_case['right_tag'] == test_case['predicted_tag']:
                test_ok += 1
        accuracy = test_ok/total
        print(f"Accuracy is {accuracy}")
        self.assertGreaterEqual(accuracy,0.7)


if __name__ == "__main__":
    test = TestResponses()
    test.test()