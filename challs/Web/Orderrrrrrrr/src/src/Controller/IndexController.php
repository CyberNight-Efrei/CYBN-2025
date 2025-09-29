<?php

namespace App\Controller;

use App\Entity\CWE;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Routing\Attribute\Route;

final class IndexController extends AbstractController
{
    #[Route('/', name: 'app_index')]
    public function index(Request $request, EntityManagerInterface $em): Response
    {
        $orderColumn = $request->query->get('column', 'e.cweId');
        $orderDirection = $request->query->get('direction', 'desc');

        $qb = $em->createQueryBuilder()
            ->select('e')
            ->from(CWE::class, 'e')
            ->orderBy($orderColumn, $orderDirection);

        return $this->render('index/list.html.twig', [
            'cwes' => $qb->getQuery()->getResult(),
            'orderColumn' => $orderColumn,
            'orderDirection' => strtoupper($orderDirection),
        ]);
    }
}
