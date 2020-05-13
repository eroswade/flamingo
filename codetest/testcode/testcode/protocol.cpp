#include "stdafx.h"
#include "protocol.h"
#include<iostream>
#include <stdio.h>
using namespace std;
#include <Winsock2.h>
#pragma comment(lib, "Ws2_32.lib")

void write7BitEncoded(uint32_t value, std::string& buf)
{
	do
	{
		unsigned char c = (unsigned char)(value & 0x7F);// 1025==> 0x81 0x08
		value >>= 7;
		if (value)
			c |= 0x80;

		buf.append(1, c);
	} while (value);
}


//=================class BinaryStreamWriter implementation============//
BinaryStreamWriter::BinaryStreamWriter(string* data) :
	m_data(data)
{
	m_data->clear();
	char str[BINARY_PACKLEN_LEN_2 + CHECKSUM_LEN];
	m_data->append(str, sizeof(str));
}
bool BinaryStreamWriter::WriteCString(const char* str, size_t len)
{
	std::string buf;
	write7BitEncoded(len, buf);

	m_data->append(buf);

	m_data->append(str, len);

	//unsigned int ulen = htonl(len);
	//m_data->append((char*)&ulen,sizeof(ulen));
	//m_data->append(str,len);
	return true;
}
bool BinaryStreamWriter::WriteString(const string& str)
{
	return WriteCString(str.c_str(), str.length());
}
const char* BinaryStreamWriter::GetData() const
{
	return m_data->data();
}
size_t BinaryStreamWriter::GetSize() const
{
	return m_data->length();
}
bool BinaryStreamWriter::WriteInt32(int32_t i, bool isNULL)
{
	int32_t i2 = 999999999;
	if (isNULL == false)
		i2 = htonl(i);
	m_data->append((char*)& i2, sizeof(i2));
	return true;
}
bool BinaryStreamWriter::WriteInt64(int64_t value, bool isNULL)
{
	char int64str[128];
	if (isNULL == false)
	{
#ifndef _WIN32
		sprintf(int64str, "%ld", value);
#else
		sprintf(int64str, "%lld", value);
#endif
		WriteCString(int64str, strlen(int64str));
	}
	else
		WriteCString(int64str, 0);
	return true;
}
bool BinaryStreamWriter::WriteShort(short i, bool isNULL)
{
	short i2 = 0;
	if (isNULL == false)
		i2 = htons(i);
	m_data->append((char*)& i2, sizeof(i2));
	return true;
}
bool BinaryStreamWriter::WriteChar(char c, bool isNULL)
{
	char c2 = 0;
	if (isNULL == false)
		c2 = c;
	(*m_data) += c2;
	return true;
}
bool BinaryStreamWriter::WriteDouble(double value, bool isNULL)
{
	char   doublestr[128];
	if (isNULL == false)
	{
		sprintf(doublestr, "%f", value);
		WriteCString(doublestr, strlen(doublestr));
	}
	else
		WriteCString(doublestr, 0);
	return true;
}
void BinaryStreamWriter::Flush()
{
	char* ptr = &(*m_data)[0];
	unsigned int ulen = htonl(m_data->length());
	memcpy(ptr, &ulen, sizeof(ulen));
}
void BinaryStreamWriter::Clear()
{
	m_data->clear();
	char str[BINARY_PACKLEN_LEN_2 + CHECKSUM_LEN];
	m_data->append(str, sizeof(str));
}