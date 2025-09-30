<?php

namespace App\DataFixtures;

use App\Entity\Flag;
use Doctrine\Bundle\FixturesBundle\Fixture;
use Doctrine\Persistence\ObjectManager;

class FlagSeeder extends Fixture
{
    public function load(ObjectManager $manager): void
    {
        $flag = $_ENV['FLAG'] ?? 'CYBN{flag}';

        $entity = new Flag();
        $entity->setFlag($flag);

        $manager->persist($entity);
        $manager->flush();
    }
}
