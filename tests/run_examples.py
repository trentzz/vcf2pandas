from vcf2pandas.vcf2pandas import vcf2pandas


def run_examples():
    process_vcf1()
    process_vcf2()
    process_vcf3_all()
    process_vcf3_all_remove_empty_columns()
    process_vcf3_selected()
    process_vcf3_everything_renamed()
    process_vcf3_sample_and_format_renamed()
    process_vcf3_sample_list_format_dict_renamed()


def process_vcf1():
    df1_all = vcf2pandas("examples/vcf1.vcf")
    with open("examples/vcf1_all.txt", "w", encoding="utf-8") as f:
        f.write(df1_all.to_string())


def process_vcf2():
    df2_all = vcf2pandas("examples/vcf2.vcf")
    with open("examples/vcf2_all.txt", "w", encoding="utf-8") as f:
        f.write(df2_all.to_string())


def process_vcf3_all():
    df3_all = vcf2pandas("examples/vcf3.vcf")
    with open("examples/vcf3_all.txt", "w", encoding="utf-8") as f:
        f.write(df3_all.to_string())
        
def process_vcf3_all_remove_empty_columns():
    df3_all = vcf2pandas("examples/vcf3.vcf", remove_empty_columns=True)
    with open("examples/vcf3_all_remove_empty_columns.txt", "w", encoding="utf-8") as f:
        f.write(df3_all.to_string())


def process_vcf3_selected():
    info_fields = ["DP"]
    sample_list = ["HG002"]
    format_fields = ["GT", "AO"]

    df3_selected = vcf2pandas(
        "examples/vcf3.vcf",
        info_fields=info_fields,
        sample_list=sample_list,
        format_fields=format_fields,
    )

    with open("examples/vcf3_selected.txt", "w", encoding="utf-8") as f:
        f.write(df3_selected.to_string())


def process_vcf3_everything_renamed():
    info_fields_dict = {"DP": "Depth"}
    sample_list_dict = {"HG002": "Sample1"}
    format_fields_dict = {"GT": "Genotype", "AO": "Allele_Observed"}

    df3_renamed = vcf2pandas(
        "examples/vcf3.vcf",
        info_fields=info_fields_dict,
        sample_list=sample_list_dict,
        format_fields=format_fields_dict,
    )

    with open("examples/vcf3_everything_renamed.txt", "w", encoding="utf-8") as f:
        f.write(df3_renamed.to_string())


def process_vcf3_sample_and_format_renamed():
    sample_list_dict = {"HG002": "Sample1"}
    format_fields_dict = {"GT": "Genotype", "AO": "Allele_Observed"}

    df3_renamed = vcf2pandas(
        "examples/vcf3.vcf",
        sample_list=sample_list_dict,
        format_fields=format_fields_dict,
    )

    with open("examples/vcf3_sample_and_format_renamed.txt", "w", encoding="utf-8") as f:
        f.write(df3_renamed.to_string())


def process_vcf3_sample_list_format_dict_renamed():
    sample_list = ["HG002"]
    format_fields_dict = {"GT": "Genotype", "AO": "Allele_Observed"}

    df3_renamed = vcf2pandas(
        "examples/vcf3.vcf",
        sample_list=sample_list,
        format_fields=format_fields_dict,
    )

    with open("examples/vcf3_sample_list_format_dict_renamed.txt", "w", encoding="utf-8") as f:
        f.write(df3_renamed.to_string())


if __name__ == "__main__":
    run_examples()
