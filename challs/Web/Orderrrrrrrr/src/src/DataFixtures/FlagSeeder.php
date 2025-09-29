<?php

namespace App\DataFixtures;

use App\Entity\Flag;
use Doctrine\Bundle\FixturesBundle\Fixture;
use Doctrine\Persistence\ObjectManager;
use RuntimeException;

class FlagSeeder extends Fixture
{
    private const FLAG = 'CYBN{flag}';

    public function load(ObjectManager $manager): void
    {
        $entity = new Flag();
        $entity->setFlag(self::FLAG);

        $manager->persist($entity);
        $manager->flush();
    }
}
