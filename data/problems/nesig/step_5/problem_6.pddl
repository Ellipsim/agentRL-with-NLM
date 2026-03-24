(define (problem problem_6)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 obj5 obj6 obj7 obj8 obj9 obj10 obj11 obj12 obj13 obj14 - block
)

(:init
	(clear obj0)
	(clear obj3)
	(clear obj4)
	(clear obj6)
	(clear obj7)
	(clear obj9)
	(clear obj10)
	(clear obj13)
	(clear obj14)
	(handempty)
	(on obj2 obj1)
	(on obj4 obj2)
	(on obj6 obj5)
	(on obj10 obj8)
	(on obj12 obj11)
	(on obj13 obj12)
	(ontable obj0)
	(ontable obj1)
	(ontable obj3)
	(ontable obj5)
	(ontable obj7)
	(ontable obj8)
	(ontable obj9)
	(ontable obj11)
	(ontable obj14)
)

(:goal (and
	(on obj2 obj1)
	(on obj4 obj2)
	(on obj10 obj13)
	(on obj12 obj11)
	(on obj13 obj12)
))
)