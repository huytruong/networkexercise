__author__ = 'hrua'
import re

class Message():

    def __init__(self, mtype=None, mid='',mpayload=""):
        self.type=mtype
        self.id = mid
        self.payload=mpayload
        self.len=0
        self.parser(mpayload)

    def parser(self,buf):
        consumed=0
        match=re.match("(?P<type>\w+) (?P<len>\w+) (?P<id>\w+)\\n", buf)
        if match:
            size_command= match.end()
            type = match.groupdict()["type"]
            m_len = int(match.groupdict()["len"])
            id = match.groupdict()["id"]
            payload=buf[size_command:]
            if len(buf) > size_command + m_len:
                payload=buf[size_command: size_command+ m_len]
                consumed = size_command+m_len

            self.type=type
            self.payload = payload
            self.id = id
            self.len = m_len
        return consumed

    def __str__(self):
        return "%s %d %s\n%s"%(self.type,len(self.payload), self.id, self.payload)





