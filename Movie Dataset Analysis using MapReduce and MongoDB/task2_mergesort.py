from mrjob.job import MRJob
from mrjob.protocol import RawValueProtocol

class MergeSortMRJob(MRJob):
    INPUT_PROTOCOL = RawValueProtocol

    def mapper(self, _, line):
        # Split the line into year, company, and count
        year_company, count = line.split('\t')
        yield int(count), year_company

    def reducer(self, count, year_companies):
        for year_company in year_companies:
            yield year_company, count

if __name__ == '__main__':
    MergeSortMRJob.run()

