from __future__ import annotations
import random
from typing import Optional


class SerialNumber(str):
    """Represents a serial number expressed in the ANSI/CTA-2063-A Physical Serial Number format."""

    length_code_points = "123456789ABCDEF"
    code_points = "0123456789ABCDEFGHJKLMNPQRSTUVWXYZ"

    @property
    def manufacturer_code(self) -> str:
        return self[0:4]

    @property
    def length_code(self) -> str:
        return self[4:5]

    @property
    def manufacturer_serial_number(self) -> str:
        return self[5:]

    @property
    def valid(self) -> bool:
        if len(self) < 6:
            return False
        if not all(c in SerialNumber.code_points for c in self.manufacturer_code):
            return False
        if self.length_code not in SerialNumber.length_code_points:
            return False
        manufacturer_serial_number_length = (
            SerialNumber.length_code_points.index(self.length_code) + 1
        )
        if manufacturer_serial_number_length != len(self.manufacturer_serial_number):
            return False
        return True

    def make_invalid_by_changing_payload_length(self, r: Optional[random.Random] = None) -> SerialNumber:
        """Generates an invalid serial number similar to this serial number."""
        if r is None:
            r = random
        my_length = self.length_code
        lengths_except_mine = [
            c for c in SerialNumber.length_code_points if c != my_length
        ]
        new_length_code = r.choice(lengths_except_mine)
        k = SerialNumber.length_code_points.index(new_length_code) + 1
        while True:
            random_serial_number = "".join(r.choices(SerialNumber.code_points, k=k))
            result = SerialNumber(
                self.manufacturer_code + self.length_code + random_serial_number
            )
            if not result.valid:
                return result

    @staticmethod
    def from_components(
        manufacturer_code: str, manufacturer_serial_number: str
    ) -> SerialNumber:
        """Constructs a standard serial number from the provided components"""
        length_code = SerialNumber.length_code_points[
            len(manufacturer_serial_number) - 1
        ]
        return SerialNumber(
            manufacturer_code + length_code + manufacturer_serial_number
        )

    @staticmethod
    def generate_valid(r: Optional[random.Random] = None) -> SerialNumber:
        """Generates a valid and random UAV serial number per ANSI/CTA-2063-A."""
        if r is None:
            r = random
        manufacturer_code = "".join(r.choices(SerialNumber.code_points, k=4))
        k = r.randrange(0, len(SerialNumber.length_code_points)) + 1
        random_serial_number = "".join(r.choices(SerialNumber.code_points, k=k))
        return SerialNumber.from_components(manufacturer_code, random_serial_number)
