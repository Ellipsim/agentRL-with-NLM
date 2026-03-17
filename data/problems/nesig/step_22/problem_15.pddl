(define (problem problem_15)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 obj5 obj6 obj7 obj8 obj9 obj10 obj11 obj12 - block
)

(:init
	(clear obj0)
	(clear obj1)
	(clear obj4)
	(clear obj5)
	(clear obj8)
	(clear obj12)
	(handempty)
	(on obj3 obj2)
	(on obj4 obj3)
	(on obj7 obj6)
	(on obj8 obj7)
	(on obj10 obj9)
	(on obj11 obj10)
	(on obj12 obj11)
	(ontable obj0)
	(ontable obj1)
	(ontable obj2)
	(ontable obj5)
	(ontable obj6)
	(ontable obj9)
)

(:goal (and
	(on obj7 obj6)
	(on obj11 obj7)
))
)