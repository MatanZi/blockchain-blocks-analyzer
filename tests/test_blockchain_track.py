from blockchain_blocks_analyzer.Config import Config
from blockchain_blocks_analyzer.Config import print_json_to_file


def test_generate_record():
    from blockchain_blocks_analyzer.blockchain_track import generate_record
    import json
    sample_out = json.load(open('../out/api_sample.json'))
    out = generate_record(json_file=sample_out)
    print_json_to_file(filename=sample_out['address'], content=out)
