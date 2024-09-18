from src.convert import convert_m4a_to_wav

def main(input_m4a):
    wav_file = "temp_audio.wav"
    convert_m4a_to_wav(input_m4a,wav_file)


if __name__ == "__main__":
    input_m4a = "videoplayback.m4a"

    main (input_m4a)