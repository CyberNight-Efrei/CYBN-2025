<?php

namespace App\DataFixtures;

use App\Entity\CWE;
use Doctrine\Bundle\FixturesBundle\Fixture;
use Doctrine\Persistence\ObjectManager;
use ZipArchive;
use RuntimeException;

class CWESeeder extends Fixture
{
    private const CWE_ZIP_PATH = __DIR__ . '/data/cwec_latest.xml.zip';

    public function load(ObjectManager $manager): void
    {
        if (!file_exists(self::CWE_ZIP_PATH)) {
            throw new RuntimeException('CWE data file not found at ' . self::CWE_ZIP_PATH);
        }

        $zip = new ZipArchive();
        if ($zip->open(self::CWE_ZIP_PATH) !== true) {
            throw new RuntimeException('Unable to open CWE zip archive.');
        }

        $xmlFile = null;
        for ($i = 0; $i < $zip->numFiles; $i++) {
            $name = $zip->getNameIndex($i);
            if (str_ends_with(strtolower($name), '.xml')) {
                $xmlFile = $zip->getFromIndex($i);
                break;
            }
        }
        $zip->close();

        if (!$xmlFile) {
            throw new RuntimeException('No XML file found in CWE zip.');
        }

        libxml_use_internal_errors(true);
        $xml = simplexml_load_string($xmlFile);
        if ($xml === false) {
            throw new RuntimeException('Failed to parse CWE XML');
        }

        $xml->registerXPathNamespace('cwe', 'http://cwe.mitre.org/cwe-7');

        $weaknesses = $xml->xpath('//cwe:Weaknesses/cwe:Weakness');
        if (!$weaknesses) {
            throw new RuntimeException('No <Weakness> nodes found in CWE XML.');
        }

        $table = $manager->getClassMetadata(CWE::class)->getTableName();
        $manager->getConnection()->executeStatement('DELETE FROM ' . $table);

        foreach ($weaknesses as $w) {
            $cweId = (int) $w['ID'];
            $name = (string) $w['Name'];
            $description = isset($w->Description) ? trim((string) $w->Description) : null;

            $entity = new CWE();
            $entity->setCweId($cweId);
            $entity->setName($name);
            $entity->setDescription($description);

            $manager->persist($entity);
        }

        $manager->flush();
    }
}
