import { CesarEncryptor, CesarDecryptor } from "./cesarCrypto";

const firstLab = () => {
  console.clear();
  const message = "London - the capital of Great Britain!".toUpperCase();

  console.log(`Исходное сообщение: ${message}`);
  const encryptor = new CesarEncryptor(message);
  const encryptedMessage = encryptor.encrypt();
  console.log(`Зашифрованное сообщение: ${encryptedMessage}`);

  const decryptor = new CesarDecryptor(encryptedMessage);
  const decryptedMessage = decryptor.decrypt();
  console.log(`Расшифрованное сообщение: ${decryptedMessage}`);
};

export { firstLab };
