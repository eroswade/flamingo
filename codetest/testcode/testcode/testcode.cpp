// testcode.cpp : 定义控制台应用程序的入口点。
//

#include "stdafx.h"
#include "protocol.h"
//typedef unsigned int       uint32_t;

#include<iostream>
#include "ZlibUtil.h"

using namespace std;

struct msg
{
	char     compressflag;     //压缩标志，如果为1，则启用压缩，反之不启用压缩
	int32_t  originsize;       //包体压缩前大小
	int32_t  compresssize;     //包体压缩后大小
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

