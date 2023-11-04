#!/usr/bin/env python

import os
import pikepdf


def is_pdf(file_path: str) -> bool:
    return os.path.splitext(file_path.lower())[1] == ".pdf"


def is_pdf_encrypted(file_path: str) -> bool:
    try:
        with pikepdf.open(file_path) as pdf:
            return pdf.is_encrypted
    except:
        return True


def pdf_has_attachments(file_path: str) -> bool:
    try:
        with pikepdf.open(file_path) as pdf:
            return len(pdf.attachments) > 0
    except:
        return False


def unlock_pdf(file_path: str) -> None:
    password = None
    print("Reading passwords from {pf}".format(pf=pass_file_path))
    with open(pass_file_path, "r") as f:
        passwords = f.readlines()
    for p in passwords:
        password = p.strip()
        try:
            with pikepdf.open(
                file_path, password=password, allow_overwriting_input=True
            ) as pdf:
                print(
                    "Unlocked succesfully with password {f}***{l}".format(
                        f=password[0], l=password[-1]
                    )
                )
                pdf.save(file_path)
                break
        except pikepdf.PasswordError:
            print(
                "Password {f}***{l} is not working".format(
                    f=password[0], l=password[-1]
                )
            )
            continue
    if password is None:
        print("Empty password file {pf}".format(pf=pass_file_path))


def extract_pdf_attachments(file_path: str) -> None:
    with pikepdf.open(file_path) as pdf:
        ats = pdf.attachments
        for atm in ats:
            trg_filename = ats.get(atm).filename
            if is_pdf(trg_filename):
                trg_file_path = os.path.join(consume_path, trg_filename)
                try:
                    with open(trg_file_path, "wb") as wb:
                        wb.write(ats.get(atm).obj["/EF"]["/F"].read_bytes())
                        print("Saved file {tf}".format(tf=trg_filename))
                except:
                    print("Error saving file {tf}".format(tf=trg_filename))
                    continue
            else:
                print("Skipped file {tf}".format(tf=trg_filename))


src_file_path = os.environ.get("DOCUMENT_WORKING_PATH")
pass_file_path = "/usr/src/paperless/scripts/passwords.txt"
consume_path = "/usr/src/paperless/consume/"

if src_file_path is None:
    print("No file path {sfp}".format(sfp=src_file_path))
    exit(0)

if not is_pdf(src_file_path):
    print("Not pdf file {sfp}".format(sfp=src_file_path))
    exit(0)

if is_pdf_encrypted(src_file_path):
    print("Decrypting pdf file {sfp}".format(sfp=src_file_path))
    unlock_pdf(src_file_path)
else:
    print("Not encrypted file {sfp}".format(sfp=src_file_path))

if pdf_has_attachments(src_file_path):
    print("Getting attachments from file {sfp}".format(sfp=src_file_path))
    extract_pdf_attachments(src_file_path)
else:
    print("No attachments in file {sfp}".format(sfp=src_file_path))