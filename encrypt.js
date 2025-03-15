window=this;
const JSEncrypt = require('jsencrypt')

//加密获得密文，key公钥，str签名
function getCode(key, str) {
    var encrypt = new JSEncrypt()
    encrypt.setPublicKey(key)
    var data = encrypt.encrypt(str)
    return data;
}

//解密获得明文，key私钥，str加密后的签名
function deCode(key, str) {
    var encrypt = new JSEncrypt()
    encrypt.setPrivateKey(key)
    var data = encrypt.decrypt(str)
    return data;
}

console.log(getCode('%KEY%', '%PASSWD%'));
