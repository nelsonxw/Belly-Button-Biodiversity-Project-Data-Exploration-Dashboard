# import dependencies
import os
import pandas as pd
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

# set up Flask
app = Flask(__name__)


# define different routes
@app.route("/")
def home():
    # render dashboard homepage
    return render_template("index.html")

@app.route("/names")
def names():
    # read data into pandas and return jsonified data
    file_name = os.path.join("datasets","belly_button_biodiversity_samples.csv")
    df = pd.read_csv(file_name)
    sample_data = df.set_index("otu_id").keys()
    return jsonify(sample_data.tolist())

@app.route("/otu")
def otu_descriptions():
    # read data into pandas and return jsonified data
    file_name = os.path.join("datasets","belly_button_biodiversity_otu_id.csv")
    df = pd.read_csv(file_name)
    otu_descriptions = df["lowest_taxonomic_unit_found"]
    return jsonify(otu_descriptions.tolist())

@app.route("/metadata/<sample>")
def metadata(sample):
    # read data into pandas and return jsonified data
    sampleID = sample[3:]
    file_name = os.path.join("datasets","Belly_Button_Biodiversity_Metadata.csv")
    df = pd.read_csv(file_name)
    meta_data = df[df["SAMPLEID"] == int(sampleID)][["SAMPLEID","ETHNICITY","GENDER","AGE","BBTYPE","LOCATION"]]
    return jsonify(meta_data.to_dict("records"))


@app.route("/wfreq/<sample>")
def washFrequency(sample):
    # read data into pandas and return jsonified data
    sampleID = sample[3:]
    file_name = os.path.join("datasets","Belly_Button_Biodiversity_Metadata.csv")
    df = pd.read_csv(file_name)
    wash_data = df[df["SAMPLEID"] == int(sampleID)]["WFREQ"].astype(int)
    return jsonify(wash_data.tolist())

@app.route("/samples/<sample>")
def samples(sample):
    # read data into pandas and return jsonified data
    file_name1 = os.path.join("datasets","belly_button_biodiversity_samples.csv")
    df_samples = pd.read_csv(file_name1)
    
    file_name2 = os.path.join("datasets","belly_button_biodiversity_otu_id.csv")
    df_otu = pd.read_csv(file_name2)
    
    df = df_samples.merge(df_otu,how="left")
    df = df[df[sample] > 0]
    # sort data by sample value, descending
    samples = df[["otu_id","lowest_taxonomic_unit_found",sample]].sort_values(sample,ascending=False)
    samples.columns = ["otu_id","otu_descriptions","sampleValue"]
    samples = [samples.to_dict("list")]
    return jsonify(samples)


if __name__ == '__main__':

    env_port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=env_port, debug=True)

