(define (problem problem_5)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 obj5 obj6 obj7 obj8 obj9 obj10 obj11 obj12 - block
)

(:init
	(clear obj4)
	(clear obj8)
	(clear obj10)
	(clear obj12)
	(handempty)
	(on obj2 obj1)
	(on obj3 obj0)
	(on obj4 obj3)
	(on obj5 obj2)
	(on obj7 obj6)
	(on obj8 obj7)
	(on obj9 obj5)
	(on obj11 obj9)
	(on obj12 obj11)
	(ontable obj0)
	(ontable obj1)
	(ontable obj6)
	(ontable obj10)
)

(:goal (and
	(on obj2 obj1)
	(on obj3 obj0)
	(on obj4 obj3)
	(on obj5 obj2)
	(on obj7 obj6)
	(on obj8 obj4)
	(on obj9 obj5)
	(on obj11 obj9)
))
)