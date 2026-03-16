(define (problem problem_16)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 obj5 obj6 obj7 obj8 obj9 obj10 obj11 obj12 - block
)

(:init
	(clear obj0)
	(clear obj2)
	(clear obj4)
	(clear obj5)
	(clear obj6)
	(clear obj7)
	(clear obj10)
	(clear obj11)
	(clear obj12)
	(handempty)
	(on obj2 obj1)
	(on obj4 obj3)
	(on obj9 obj8)
	(on obj10 obj9)
	(ontable obj0)
	(ontable obj1)
	(ontable obj3)
	(ontable obj5)
	(ontable obj6)
	(ontable obj7)
	(ontable obj8)
	(ontable obj11)
	(ontable obj12)
)

(:goal (and
	(on obj2 obj1)
))
)