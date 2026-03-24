(define (problem problem_9)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 obj5 obj6 obj7 obj8 obj9 obj10 obj11 obj12 obj13 - block
)

(:init
	(clear obj2)
	(clear obj4)
	(clear obj5)
	(clear obj7)
	(clear obj8)
	(clear obj13)
	(handempty)
	(on obj1 obj0)
	(on obj2 obj1)
	(on obj5 obj3)
	(on obj8 obj6)
	(on obj10 obj9)
	(on obj11 obj10)
	(on obj12 obj11)
	(on obj13 obj12)
	(ontable obj0)
	(ontable obj3)
	(ontable obj4)
	(ontable obj6)
	(ontable obj7)
	(ontable obj9)
)

(:goal (and
	(on obj1 obj0)
	(on obj2 obj7)
	(on obj5 obj3)
	(on obj8 obj6)
	(on obj10 obj9)
	(on obj11 obj10)
	(on obj12 obj11)
	(on obj13 obj12)
))
)