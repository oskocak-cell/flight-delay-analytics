"""Check publication safety and basic structure; does not execute Pentaho."""
from pathlib import Path
import xml.etree.ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    files = sorted((ROOT / 'pentaho/transformations').glob('*.ktr'))
    require(len(files) == 5, 'Expected five original transformations')
    for file in files:
        root = ET.parse(file).getroot()
        steps = {step.findtext('name') for step in root.findall('step')}
        for hop in root.findall('order/hop'):
            require(hop.findtext('from') in steps and hop.findtext('to') in steps,
                    f'{file.name}: invalid step connection')
        for conn in root.findall('connection'):
            require(not conn.findtext('password') and not conn.findtext('username'),
                    f'{file.name}: credentials must remain blank')
            require(conn.findtext('server') == 'localhost',
                    f'{file.name}: use the documented local placeholder')
    with ZipFile(ROOT / 'pentaho/reports/airport-delay-report.prpt') as archive:
        require(archive.testzip() is None, 'Report archive integrity failed')
        for name in archive.namelist():
            if not name.endswith('.xml'):
                continue
            root = ET.fromstring(archive.read(name))
            for node in root.iter():
                if node.tag.split('}')[-1] == 'property' and node.get('name') in ('user', 'password'):
                    require(not (node.text or '').strip(), 'Report credentials must remain blank')
                if node.tag.split('}')[-1] == 'url' and name == 'datasources/sql-ds.xml':
                    require(node.text == 'jdbc:mysql://localhost:3306/dw_airline',
                            'Use the documented local report JDBC placeholder')
    print('Five transformation graphs and report XML/archive checked; connection credentials are blank.')


if __name__ == '__main__':
    main()
