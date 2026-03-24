(define (problem problem_21)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 obj5 obj6 obj7 obj8 obj9 obj10 obj11 obj12 obj13 - block
)

(:init
	(clear obj1)
	(clear obj2)
	(clear obj3)
	(clear obj6)
	(clear obj7)
	(clear obj13)
	(handempty)
	(on obj1 obj0)
	(on obj5 obj4)
	(on obj6 obj5)
	(on obj9 obj8)
	(on obj10 obj9)
	(on obj11 obj10)
	(on obj12 obj11)
	(on obj13 obj12)
	(ontable obj0)
	(ontable obj2)
	(ontable obj3)
	(ontable obj4)
	(ontable obj7)
	(ontable obj8)
)

(:goal (and
	(on obj1 obj6)
	(on obj3 obj13)
	(on obj5 obj4)
	(on obj6 obj5)
	(on obj9 obj8)
	(on obj10 obj9)
	(on obj11 obj10)
	(on obj12 obj11)
	(on obj13 obj12)
))
)