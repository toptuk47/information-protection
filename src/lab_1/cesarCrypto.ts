const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ .,!:;?-";
const shift = 3; // k

const getAlphabetIndex = (letter: string) => {
  return alphabet.split("").findIndex((item) => item == letter);
};

class CesarEncryptor {
  private message: string;

  constructor(message: string) {
    this.message = message;
  }

  public encrypt(): string {
    let result = [];

    for (let i = 0; i < this.message.length; i++) {
      const index = getAlphabetIndex(this.message[i]);
      const resultChar = alphabet[(index + shift) % alphabet.length];
      result.push(resultChar);
    }

    return result.join("");
  }
}

class CesarDecryptor {
  private message: string;

  constructor(sipheredMessage: string) {
    this.message = sipheredMessage;
  }

  public decrypt(): string {
    let result = [];

    for (let i = 0; i < this.message.length; i++) {
      const index = getAlphabetIndex(this.message[i]);
      const resultChar = alphabet.at(index - shift);
      result.push(resultChar);
    }

    return result.join("");
  }
}

export { CesarEncryptor, CesarDecryptor };
