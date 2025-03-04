import pytest

from vcf2pandas import vcf2pandas


def test_default():
    df = vcf2pandas("tests/vcfs/minimal_vcf.vcf")
    expected_columns = [
        "CHROM",
        "POS",
        "ID",
        "REF",
        "ALT",
        "QUAL",
        "FILTER",
        "INFO:INFO_FIELD",
        "INFO:EMPTY_INFO_FIELD",
        "FORMAT:SAMPLE1:FORMAT_FIELD",
        "FORMAT:SAMPLE1:EMPTY_FORMAT_FIELD",
        "FORMAT:SAMPLE2:FORMAT_FIELD",
        "FORMAT:SAMPLE2:EMPTY_FORMAT_FIELD",
    ]
    assert list(df.columns) == expected_columns


def test_remove_empty_columns():
    df = vcf2pandas("tests/vcfs/minimal_vcf.vcf", remove_empty_columns=True)
    expected_columns = [
        "CHROM",
        "POS",
        "ID",
        "REF",
        "ALT",
        "QUAL",
        "FILTER",
        "INFO:INFO_FIELD",
        "FORMAT:SAMPLE1:FORMAT_FIELD",
        "FORMAT:SAMPLE2:FORMAT_FIELD",
    ]
    assert list(df.columns) == expected_columns


def test_info_fields_list():
    info_fields = ["INFO_FIELD"]
    df = vcf2pandas("tests/vcfs/minimal_vcf.vcf", info_fields=info_fields, format_fields=[])
    expected_columns = [
        "CHROM",
        "POS",
        "ID",
        "REF",
        "ALT",
        "QUAL",
        "FILTER",
        "INFO:INFO_FIELD",
    ]
    assert list(df.columns) == expected_columns


def test_info_fields_dict():
    info_fields = {"INFO_FIELD": "Info_Field"}
    df = vcf2pandas("tests/vcfs/minimal_vcf.vcf", info_fields=info_fields, format_fields=[])
    expected_columns = [
        "CHROM",
        "POS",
        "ID",
        "REF",
        "ALT",
        "QUAL",
        "FILTER",
        "INFO:Info_Field",
    ]
    assert list(df.columns) == expected_columns


def test_sample_list_list():
    sample_list = ["SAMPLE1"]
    df = vcf2pandas("tests/vcfs/minimal_vcf.vcf", info_fields=[], sample_list=sample_list)
    expected_columns = [
        "CHROM",
        "POS",
        "ID",
        "REF",
        "ALT",
        "QUAL",
        "FILTER",
        "FORMAT:SAMPLE1:FORMAT_FIELD",
        "FORMAT:SAMPLE1:EMPTY_FORMAT_FIELD",
    ]
    assert list(df.columns) == expected_columns


def test_sample_list_dict():
    sample_list = {"SAMPLE1": "Sample1"}
    df = vcf2pandas("tests/vcfs/minimal_vcf.vcf", info_fields=[], sample_list=sample_list)
    expected_columns = [
        "CHROM",
        "POS",
        "ID",
        "REF",
        "ALT",
        "QUAL",
        "FILTER",
        "FORMAT:Sample1:FORMAT_FIELD",
        "FORMAT:Sample1:EMPTY_FORMAT_FIELD",
    ]
    assert list(df.columns) == expected_columns


def test_format_fields_list():
    format_fields = ["FORMAT_FIELD"]
    df = vcf2pandas("tests/vcfs/minimal_vcf.vcf", info_fields=[], format_fields=format_fields)
    expected_columns = [
        "CHROM",
        "POS",
        "ID",
        "REF",
        "ALT",
        "QUAL",
        "FILTER",
        "FORMAT:SAMPLE1:FORMAT_FIELD",
        "FORMAT:SAMPLE2:FORMAT_FIELD",
    ]
    assert list(df.columns) == expected_columns


def test_format_fields_dict():
    format_fields = {"FORMAT_FIELD": "Format_Field", "EMPTY_FORMAT_FIELD": "Empty_Format_Field"}
    df = vcf2pandas("tests/vcfs/minimal_vcf.vcf", info_fields=[], format_fields=format_fields)
    expected_columns = [
        "CHROM",
        "POS",
        "ID",
        "REF",
        "ALT",
        "QUAL",
        "FILTER",
        "FORMAT:SAMPLE1:Format_Field",
        "FORMAT:SAMPLE1:Empty_Format_Field",
        "FORMAT:SAMPLE2:Format_Field",
        "FORMAT:SAMPLE2:Empty_Format_Field",
    ]
    assert list(df.columns) == expected_columns
