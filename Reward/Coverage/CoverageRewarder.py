import glob
import os
import shutil
import subprocess

from Reward.AbstractRewarder import Rewarder
from Reward.Coverage.Constants import TEST_TEMPLATE


# URL1 = "http://cov-rladt.ddns.net:8112/v1/coverage"
# URL2 = "http://cov-rladt.ddns.net:8113/v1/coverage"


class CoverageRewarder(Rewarder):

    def __init__(self):
        super().__init__()

    def resolveReward(self, nameOfFunction, numOfWorker, matrixWithValues):
        # HERE ADD CLEAN BEFORE WORK
        # traceFiles = glob.glob("*.trace")
        # for filePath in traceFiles:
        #     if os.path.isfile(filePath):
        #         os.remove(filePath)
        try:
            shutil.rmtree("functions/" + numOfWorker + "/")
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))

        # try:
        #     shutil.rmtree("functions/"+numOfWorker+"/src/")
        # except OSError as e:
        #     print("Error: %s - %s." % (e.filename, e.strerror))
        os.mkdir("functions/" + numOfWorker + "/")
        os.mkdir("functions/" + numOfWorker + "/src/")

        # COPY TEST FILE  # TODO -> RETRIEVE NAME OF FUNCTION CALLS TO GET REST OF FUNCTIONS NEEDED
        shutil.copy2("functions/default.gpr", "functions/" + numOfWorker + "/")
        shutil.copy2("functions/" + nameOfFunction + ".c", "functions/" + numOfWorker + "/src")
        self.copyHeader(nameOfFunction, numOfWorker)
        if nameOfFunction == "checkingPrime":
            shutil.copy2("functions/checkPrime.c", "functions/" + numOfWorker + "/src")
            shutil.copy2("functions/checkPrime.h", "functions/" + numOfWorker + "/src")
        elif nameOfFunction == "isPrimeCheck":
            shutil.copy2("functions/isPrime.c", "functions/" + numOfWorker + "/src")
            shutil.copy2("functions/isPrime.h", "functions/" + numOfWorker + "/src")
        elif nameOfFunction == "binToOct":
            shutil.copy2("functions/three_digits.c", "functions/" + numOfWorker + "/src")
            shutil.copy2("functions/three_digits.h", "functions/" + numOfWorker + "/src")

        # PREPARE TEST FILE
        self.filePathFinal = self.getFilePath(nameOfFunction, numOfWorker)
        functionBody = self.openGivenSrcFileTex()
        testBody = self.prepareTestBody(nameOfFunction, matrixWithValues)
        testfunc = TEST_TEMPLATE.format(mainFunc=functionBody, testCalls=testBody)

        with open("functions/" + numOfWorker + "/src/test_" + nameOfFunction + ".c", "w") as text_file:
            text_file.write(testfunc)

        # COMPILE THE FUNCTION AND RUN THE TEST OBTAINING TRACE
        subprocess.check_output(
            "gprbuild -p -Pfunctions/" + numOfWorker + "/default.gpr functions/" + numOfWorker + "/src/test_" + nameOfFunction + ".c  -cargs:C -g -fpreserve-control-flow -fdump-scos",
            shell=True)
        # os.system("gnatcov run functions/obj/test_" + nameOfFunction)
        try:
            f = subprocess.check_output(
                "gnatcov run -o functions/" + numOfWorker + "/obj/test_" + nameOfFunction + ".trace functions/" + numOfWorker + "/obj/test_" + nameOfFunction,
                shell=True)
        except:
            f = "non zero status"

        if not f:
            os.system(
                "gnatcov coverage --level=stmt+uc_mcdc --annotate=xcov functions/" + numOfWorker + "/obj/test_" + nameOfFunction + ".trace -Pfunctions/" + numOfWorker + "/default.gpr")

            # RETURN THE COVERAGE
            with open("functions/" + numOfWorker + "/obj/test_" + nameOfFunction + ".c.xcov", "r") as cov_file:
                cov_file.readline()
                coverageLine = cov_file.readline()
                cov_perc = coverageLine.split("%")[0]
        else:
            cov_perc = 0

        return int(cov_perc)

    def copyHeader(self, functionName, numOfWorker):
        listOfFiles = glob.glob("functions/" + functionName + ".h")
        for filePath in listOfFiles:
            shutil.copy2(filePath, "functions/" + numOfWorker + "/src")

    def getFilePath(self, functionName, numOfWorker):
        listOfFiles = glob.glob("functions/" + numOfWorker + "/src/*.c")
        filePathFinal = None
        for filePath in listOfFiles:
            if functionName in filePath:
                filePathFinal = filePath
                break
        return filePathFinal

    def openGivenSrcFileTex(self):
        with open(self.filePathFinal, 'r') as F:
            return F.read()

    def prepareTestBody(self, nameOfFunction, matrixWithValues):
        testFunctionCalls = ""
        for row in matrixWithValues:
            call = nameOfFunction + "("
            for argument in row:
                call += str(argument) + ","
            call = call[:-1]
            call += ");" + "\n"
            testFunctionCalls += call
        return testFunctionCalls
    #
    # def run(self, numOfFile, numOfWorker, matrixWithValues):
    #     body = {'numOfFile': numOfFile,
    #             'numOfWorker': int(numOfWorker),
    #             'covMatrix': matrixWithValues}
    #
    #     req = urllib.request.Request(URL1)
    #     req.add_header('Content-Type', 'application/json; charset=utf-8')
    #
    #     jsondata = json.dumps(body)
    #     jsondataasbytes = jsondata.encode('utf-8')  # needs to be bytes
    #
    #     req.add_header('Content-Length', len(jsondataasbytes))
    #     response = urllib.request.urlopen(req, jsondataasbytes)
    #
    #     coverage = json.loads(response.read())
    #
    #     return coverage
