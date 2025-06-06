from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import nextupdb
import re
import random

class NeuralHTTP(BaseHTTPRequestHandler):
    def do_GET(self):
        if re.search("/students", self.path):
            try:
                students = nextupdb.getStudents()

                response = []

                for stud in students:
                    response.append(
                        {
                            "studentId": stud[0],
                            "studentName": stud[1],
                            "studentSurname": stud[2]
                        }
                    )

                json_resp = json.dumps(response)

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                self.wfile.write(bytes(json_resp, "utf-8"))
            except:
                self.send_response(400)
                self.end_headers()

        elif re.search("/subjects", self.path):
            try:
                subjects = nextupdb.getSubjects()

                response = []

                for subj in subjects:
                    response.append(
                        {
                            "subjectId": subj[0],
                            "subjectName": subj[1],
                            "teacher": subj[2]
                        }
                    )

                json_resp = json.dumps(response)

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                self.wfile.write(bytes(json_resp, "utf-8"))
            except:
                self.send_response(400)
                self.end_headers()
        
        elif re.search("/draw", self.path):
            try:
                msgList = nextupdb.getDraws()

                msg = []

                for stud in msgList:
                    msg.append(
                        {
                            "studentId": stud[0],
                            "subjectId": stud[1],
                            "position": stud[2]
                        }
                    )

                json_resp = json.dumps(msg)
                
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                
                self.wfile.write(bytes(json_resp, "utf-8"))
            except:
                self.send_response(400)
                self.end_headers()

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if re.search("/students", self.path):
            try:
                cont_len = int(self.headers.get('Content-Length'))
                response = json.loads(self.rfile.read(cont_len))

                nextupdb.addStudent(response["studentName"], response["studentSurname"])

                students = nextupdb.getStudents()

                response = []

                for stud in students:
                    response.append(
                        {
                            "studentId": stud[0],
                            "studentName": stud[1],
                            "studentSurname": stud[2]
                        }
                    )

                json_resp = json.dumps(response)

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                self.wfile.write(bytes(json_resp, "utf-8"))
            except:
                self.send_response(400)
                self.end_headers()

        elif re.search("/subjects", self.path):
            try:
                cont_len = int(self.headers.get('Content-Length'))
                response = json.loads(self.rfile.read(cont_len))

                nextupdb.addSubject(response["subjectName"], response["teacher"])

                subjects = nextupdb.getSubjects()

                response = []

                for subj in subjects:
                    response.append(
                        {
                            "subjectId": subj[0],
                            "subjectName": subj[1],
                            "teacher": subj[2]
                        }
                    )

                json_resp = json.dumps(response)

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                self.wfile.write(bytes(json_resp, "utf-8"))
            except:
                self.send_response(400)
                self.end_headers()
        
        elif re.search("/draw", self.path):
            try:
                cont_len = int(self.headers.get('Content-Length'))
                response = json.loads(self.rfile.read(cont_len))

                students = nextupdb.getStudents()
                subjects = nextupdb.getSubjects()
                lists = nextupdb.getDraws()

                drawSubject = response["subjectId"]
                drawNumber = response["drawNumber"]

                studNotDrawn = []
                for stud in students:
                    studNotDrawn.append(stud[0])
                
                stAlrDrwPos = []

                for stud in lists:
                    if stud[1] == drawSubject:
                        studNotDrawn.remove(stud[0])
                        stAlrDrwPos.append(stud[2])

                stAlrDrwPos.sort()

                random.shuffle(studNotDrawn)

                studDrawn = studNotDrawn[:drawNumber]

                print(studDrawn)
    
                if len(stAlrDrwPos) == 0:
                    for stud in studDrawn:
                        nextupdb.setStudDrawn(stud, drawSubject, 1 + studDrawn.index(stud))
                else:
                    for stud in studDrawn:
                        nextupdb.setStudDrawn(stud, drawSubject, stAlrDrwPos[len(stAlrDrwPos) - 1] + 1 + studDrawn.index(stud))

                msgList = nextupdb.getDraws()

                msg = []

                for stud in msgList:
                    msg.append(
                        {
                            "studentId": stud[0],
                            "subjectId": stud[1],
                            "position": stud[2]
                        }
                    )

                json_resp = json.dumps(msg)
                
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                
                self.wfile.write(bytes(json_resp, "utf-8"))
            except:
                self.send_response(400)
                self.end_headers()
        
        else:
            self.send_response(404)
            self.end_headers()

    def do_DELETE(self):
        if re.search("/students", self.path):
            try:
                cont_len = int(self.headers.get('Content-Length'))
                response = json.loads(self.rfile.read(cont_len))
                
                nextupdb.removeStudent(response["studentName"], response["studentSurname"])

                students = nextupdb.getStudents()

                response = []

                for stud in students:
                    response.append(
                        {
                            "studentId": stud[0],
                            "studentName": stud[1],
                            "studentSurname": stud[2]
                        }
                    )

                json_resp = json.dumps(response)

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                self.wfile.write(bytes(json_resp, "utf-8"))
            except:
                self.send_response(400)
                self.end_headers()

        elif re.search("/subjects", self.path):
            try:
                cont_len = int(self.headers.get('Content-Length'))
                response = json.loads(self.rfile.read(cont_len))

                nextupdb.removeSubject(response["subjectName"], response["teacher"])

                subjects = nextupdb.getSubjects()

                response = []

                for subj in subjects:
                    response.append(
                        {
                            "subjectId": subj[0],
                            "subjectName": subj[1],
                            "teacher": subj[2]
                        }
                    )

                json_resp = json.dumps(response)

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                self.wfile.write(bytes(json_resp, "utf-8"))
            except:
                self.send_response(400)
                self.end_headers()

        elif re.search("/draw", self.path):
            try:
                cont_len = int(self.headers.get('Content-Length'))
                response = json.loads(self.rfile.read(cont_len))

                nextupdb.removeDrawn(response["studentId"], response["subjectId"])

                msgList = nextupdb.getDraws()

                msg = []

                for stud in msgList:
                    msg.append(
                        {
                            "studentId": stud[0],
                            "subjectId": stud[1],
                            "position": stud[2]
                        }
                    )

                json_resp = json.dumps(msg)
                
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                
                self.wfile.write(bytes(json_resp, "utf-8"))
            except:
                self.send_response(400)
                self.end_headers()
        
        else:
            self.send_response(404)
            self.end_headers()

def startServer():
    server = HTTPServer(("", 4444), NeuralHTTP)
    print("Server Avviato....")

    server.serve_forever()
    server.server_close()