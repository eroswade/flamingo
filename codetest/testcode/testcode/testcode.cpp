// testcode.cpp : �������̨Ӧ�ó������ڵ㡣
//

#include "stdafx.h"
#include "protocol.h"
//typedef unsigned int       uint32_t;

#include<iostream>
#include "ZlibUtil.h"

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

	std::string strDestBuf;
	if (!ZlibUtil::CompressBuf(outbuf, strDestBuf))
	{
		printf("Compress error.");
		return 0 ;
	}

	int32_t length = (int32_t)outbuf.length();
	msg rems;
	rems.compressflag = 1;
	rems.compresssize = (int32_t)strDestBuf.length();
	rems.originsize = length;
	int nsize  = sizeof(rems);
	std::string m_strSendBuf;
	m_strSendBuf.append((const char*)&rems, sizeof(rems));
	m_strSendBuf.append(strDestBuf);
    return 0;
}

