import io
import pathlib
import unittest

from dm_job_utilities.utils import (
    calc_geometric_mean,
    is_type,
    read_delimiter,
    update_charge_flag_in_atom_block,
    write_row,
)

class TestUtilsMethods(unittest.TestCase):

    def test_update_charge_flag_in_atom_block(self):
        atom_block_a_in = pathlib.Path('test-data/atom-block-a-in.sdf').read_text()
        atom_block_a_out = pathlib.Path('test-data/atom-block-a-out.sdf').read_text()
        output = update_charge_flag_in_atom_block(atom_block_a_in)
        self.assertEqual(output, atom_block_a_out)

    def test_read_delimiter(self):
        self.assertEqual(read_delimiter("comma"), ",")
        self.assertEqual(read_delimiter("pipe"), "|")
        self.assertEqual(read_delimiter("space"), None)
        self.assertEqual(read_delimiter("tab"), "\t")
        self.assertEqual(read_delimiter("unknown"), "unknown")

    def test_calc_geometric_mean(self):
        data = [1.0, 2.0, 3.0, 4.0, 5.0]
        mean = calc_geometric_mean(data)
        self.assertAlmostEqual(mean, 2.605, 3)

    def test_is_type(self):
        self.assertEqual(is_type(None, int), (0, None))
        self.assertEqual(is_type(1, int), (1, 1))
        self.assertEqual(is_type("1", str), (1, '1'))
        self.assertEqual(is_type(1.0, float), (1, 1))
        self.assertEqual(is_type(1, str), (1, '1'))
        self.assertEqual(is_type("1", float), (1, 1.0))
        self.assertEqual(is_type(1.0, int), (1, 1))

    def test_write_row(self):
        out = io.StringIO()
        write_row(["a", "b,c", 1, 2.5], ",", out)
        self.assertEqual(out.getvalue(), 'a,"b,c",1,2.5\n')

    def test_write_row_with_no_embedded_delimiter(self):
        out = io.StringIO()
        write_row(["a", "b", "c"], "\t", out)
        self.assertEqual(out.getvalue(), "a\tb\tc\n")
