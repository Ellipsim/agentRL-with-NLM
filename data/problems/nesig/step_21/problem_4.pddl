(define (problem problem_4)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 obj5 obj6 obj7 obj8 obj9 obj10 obj11 obj12 obj13 obj14 - block
)

(:init
	(clear obj1)
	(clear obj3)
	(clear obj6)
	(clear obj8)
	(clear obj9)
	(clear obj10)
	(clear obj12)
	(clear obj14)
	(handempty)
	(on obj1 obj0)
	(on obj3 obj2)
	(on obj5 obj4)
	(on obj6 obj5)
	(on obj8 obj7)
	(on obj12 obj11)
	(on obj14 obj13)
	(ontable obj0)
	(ontable obj2)
	(ontable obj4)
	(ontable obj7)
	(ontable obj9)
	(ontable obj10)
	(ontable obj11)
	(ontable obj13)
)

(:goal (and
	(on obj3 obj2)
	(on obj5 obj4)
	(on obj6 obj8)
	(on obj8 obj7)
	(on obj14 obj13)
))
)