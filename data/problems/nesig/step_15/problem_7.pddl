(define (problem problem_7)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 obj5 obj6 obj7 obj8 obj9 obj10 obj11 obj12 obj13 obj14 - block
)

(:init
	(clear obj0)
	(clear obj1)
	(clear obj2)
	(clear obj4)
	(clear obj5)
	(clear obj7)
	(clear obj11)
	(clear obj13)
	(clear obj14)
	(handempty)
	(on obj4 obj3)
	(on obj7 obj6)
	(on obj9 obj8)
	(on obj10 obj9)
	(on obj11 obj10)
	(on obj13 obj12)
	(ontable obj0)
	(ontable obj1)
	(ontable obj2)
	(ontable obj3)
	(ontable obj5)
	(ontable obj6)
	(ontable obj8)
	(ontable obj12)
	(ontable obj14)
)

(:goal (and
	(on obj7 obj6)
	(on obj9 obj8)
	(on obj10 obj9)
	(on obj11 obj10)
	(on obj13 obj12)
))
)