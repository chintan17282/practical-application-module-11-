import apache_beam as beam
import requests
import argparse
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions

def process(element):
    data = element.split(',')
    vin = data[12]
    if len(vin) == 0:
        return None

    url = f'https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvaluesextended/{vin}?format=json'
    r = requests.get(url)
    try:
        response = r.json()

        # VIN_,BodyClass,Doors,DriveType,EngineCylinders,FuelTypePrimary,TransmissionStyle,Make
        return ",".join([f"{vin}",
                         response['Results'][0]['BodyClass'].split("/")[0].lower(),
                         response['Results'][0]['Doors'],
                         response['Results'][0]['DriveType'].split("/")[0].lower(),
                         response['Results'][0]['EngineCylinders'],
                         response['Results'][0]['FuelTypePrimary'],
                         response['Results'][0]['TransmissionStyle'].split("/")[0].lower(),
                         response['Results'][0]['Make'].lower()])

    except Exception as e:
        print(e)
        return None


def run(argv=None, save_main_session=True):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input',
        dest='input',
        help='Input file to process.')

    parser.add_argument(
        '--output',
        dest='output',
        required=True,
        help='Output file to write results to.')

    known_args, pipeline_args = parser.parse_known_args(argv)

    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = save_main_session

    with beam.Pipeline(options=pipeline_options) as pipeline:
        lines = pipeline | beam.io.ReadFromText(known_args.input, skip_header_lines=1)
        processed_lines = lines | beam.Map(process)
        processed_lines | beam.io.WriteToText(known_args.output)


if __name__ == '__main__':
    run()
