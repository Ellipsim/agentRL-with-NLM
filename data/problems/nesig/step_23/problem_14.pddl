(define (problem problem_14)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 obj5 obj6 obj7 obj8 obj9 obj10 obj11 obj12 - block
)

(:init
	(clear obj1)
	(clear obj4)
	(clear obj5)
	(clear obj9)
	(clear obj10)
	(clear obj12)
	(handempty)
	(on obj1 obj0)
	(on obj3 obj2)
	(on obj4 obj3)
	(on obj7 obj6)
	(on obj8 obj7)
	(on obj9 obj8)
	(on obj12 obj11)
	(ontable obj0)
	(ontable obj2)
	(ontable obj5)
	(ontable obj6)
	(ontable obj10)
	(ontable obj11)
)

(:goal (and
	(on obj1 obj0)
	(on obj7 obj6)
	(on obj8 obj1)
	(on obj9 obj3)
))
)