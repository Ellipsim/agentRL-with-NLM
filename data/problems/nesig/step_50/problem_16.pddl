(define (problem problem_16)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 obj5 obj6 obj7 obj8 obj9 obj10 obj11 obj12 obj13 obj14 obj15 - block
)

(:init
	(clear obj0)
	(clear obj3)
	(clear obj4)
	(clear obj9)
	(clear obj15)
	(handempty)
	(on obj2 obj1)
	(on obj3 obj2)
	(on obj6 obj5)
	(on obj7 obj6)
	(on obj8 obj7)
	(on obj9 obj8)
	(on obj11 obj10)
	(on obj12 obj11)
	(on obj13 obj12)
	(on obj14 obj13)
	(on obj15 obj14)
	(ontable obj0)
	(ontable obj1)
	(ontable obj4)
	(ontable obj5)
	(ontable obj10)
)

(:goal (and
	(on obj6 obj5)
	(on obj7 obj6)
	(on obj11 obj10)
	(on obj12 obj11)
	(on obj13 obj12)
	(on obj14 obj13)
	(on obj15 obj14)
))
)