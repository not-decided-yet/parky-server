"""Toolset for implementing V2D authentication."""


class V2DService:
    @staticmethod
    def get_public_key_by_uid(uid: str) -> str:
        """
        Retrieve public key of given user.

        :param uid: User ID
        :returns: PEM-style public key
        """
        pass

    @staticmethod
    def verify_signature(message: str, public_key: str) -> str:
        """
        Verify signature by given public_key, and returns the message.

        :param message: Encrypted message
        :param public_key: User's public key obtained from backend
        :returns: Message
        """
        pass

    @staticmethod
    def get_second_token_by_first_token(uid: str, vid: str, first_token: str) -> str:
        """
        Retrieve second secret token by using first token.

        :param uid: User ID
        :param vid: Vehicle ID
        :param first_token: $$T_1$$
        :returns: $$T_2$$
        """
        pass

    @staticmethod
    def sign_message(message: str, private_key: str) -> str:
        """
        Sign message by using private key.

        :param message: Message to sign
        :param private_key: Vehicle's private key
        :returns: Signed message
        """
        pass
