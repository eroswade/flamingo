#pragma once

enum
{
	TEXT_PACKLEN_LEN = 4,
	TEXT_PACKAGE_MAXLEN = 0xffff,
	BINARY_PACKLEN_LEN = 2,
	BINARY_PACKAGE_MAXLEN = 0xffff,

	TEXT_PACKLEN_LEN_2 = 6,
	TEXT_PACKAGE_MAXLEN_2 = 0xffffff,

	BINARY_PACKLEN_LEN_2 = 4,               //4字节头长度
	BINARY_PACKAGE_MAXLEN_2 = 0x10000000,   //包最大长度是256M,足够了

	CHECKSUM_LEN = 2,
};

class BinaryStreamWriter final
{
public:
	BinaryStreamWriter(std::string* data);
	~BinaryStreamWriter() = default;

	virtual const char* GetData() const;
	virtual size_t GetSize() const;
	bool WriteCString(const char* str, size_t len);
	bool WriteString(const std::string& str);
	bool WriteDouble(double value, bool isNULL = false);
	bool WriteInt64(int64_t value, bool isNULL = false);
	bool WriteInt32(int32_t i, bool isNULL = false);
	bool WriteShort(short i, bool isNULL = false);
	bool WriteChar(char c, bool isNULL = false);
	size_t GetCurrentPos() const { return m_data->length(); }
	void Flush();
	void Clear();

private:
	BinaryStreamWriter(const BinaryStreamWriter&) = delete;
	BinaryStreamWriter& operator=(const BinaryStreamWriter&) = delete;

private:
	std::string* m_data;
};