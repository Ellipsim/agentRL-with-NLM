(define (problem problem_4)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 obj5 obj6 obj7 obj8 obj9 obj10 obj11 obj12 - block
)

(:init
	(clear obj0)
	(clear obj3)
	(clear obj6)
	(clear obj8)
	(clear obj12)
	(handempty)
	(on obj2 obj1)
	(on obj3 obj2)
	(on obj5 obj4)
	(on obj6 obj5)
	(on obj8 obj7)
	(on obj10 obj9)
	(on obj11 obj10)
	(on obj12 obj11)
	(ontable obj0)
	(ontable obj1)
	(ontable obj4)
	(ontable obj7)
	(ontable obj9)
)

(:goal (and
	(on obj5 obj4)
	(on obj8 obj7)
	(on obj10 obj9)
))
)