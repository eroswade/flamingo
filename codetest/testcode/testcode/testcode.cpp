// testcode.cpp : �������̨Ӧ�ó������ڵ㡣
//

#include "stdafx.h"
#include "protocol.h"
//typedef unsigned int       uint32_t;

#include<iostream>

using namespace std;

struct msg
{
	char     compressflag;     //ѹ����־�����Ϊ1��������ѹ������֮������ѹ��
	int32_t  originsize;       //����ѹ��ǰ��С
	int32_t  compresssize;     //����ѹ�����С
	char     reserved[16];
};

int main()
{
	char* pszUser = "13575982163";
	char* pszPassword = "sunshower";
	int nClientType = 1;
	int nOnlineStatus = 1;
	
	char szLoginInfo[256] = { 0 };
	sprintf_s(szLoginInfo,
		ARRAYSIZE(szLoginInfo),
		"{\"username\": \"%s\", \"password\": \"%s\", \"clienttype\": %d, \"status\": %d}",
		pszUser,
		pszPassword,
		nClientType,
		nOnlineStatus);

	string outbuf;
	BinaryStreamWriter writeStream(&outbuf);
	writeStream.WriteInt32(1002);
	writeStream.WriteInt32(0);
	writeStream.WriteCString(szLoginInfo, strlen(szLoginInfo));//
	writeStream.Flush();

	msg rems;
	rems.compressflag = 1;
	rems.compresssize = 91;
	rems.originsize = 97;
	int nsize  = sizeof(rems);
	std::string m_strSendBuf;
	m_strSendBuf.append((const char*)&rems, sizeof(rems));
    return 0;
}

