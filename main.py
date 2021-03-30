from src.gmaillabelcreate import gmaillabel
import argparse

def main(label_name, label_color=None, label_delete=False):
    gmaillabel.main(label_name, label_color=label_color, label_delete=label_delete)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage the labels at gmail account")
    parser.add_argument("-t", "--title", help="Label tytle, (str)",
                    type=str, default="Job Applications")
    parser.add_argument("-st", "--subtitle", help="Label subtytle, (str). Note, the label name will be composed from title and subtitle as: 'title/subtitle'.",
                    type=str, default=None)
    parser.add_argument("-status", "--status", type=str, choices=["pending", "fail", "success"],
                    help="Set a status of a label, (str). Defines the label color.", 
                    default="pending")
    parser.add_argument("-d", "--delete", help="Delete a label, (bool)",
                    action="store_true")
    args = parser.parse_args()

    label_title = args.title
    label_subtitle = args.subtitle
    label_status = args.status
    ifdelete = args.delete

    label_name = label_title
    if label_subtitle:
        label_name += "/{}".format(label_subtitle)

    label_color = gmaillabel.color_dict[label_status]
    main(label_name, label_color=label_color, label_delete=ifdelete)
