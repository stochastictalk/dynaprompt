from dynaprompt import DynaPrompt

def check_recognizes_dps(dp: DynaPrompt):
    dp._parse_message(
        """dps user tomorrow afternoon
        some bullshit"""
    )

def check_recognizes_dpd(dp: DynaPrompt):


def test_DynaPrompt():

    dp = DynaPrompt()

    