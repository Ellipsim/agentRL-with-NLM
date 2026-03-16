

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(on b1 b5)
(ontable b2)
(on b3 b9)
(ontable b4)
(ontable b5)
(on b6 b7)
(ontable b7)
(on b8 b2)
(ontable b9)
(clear b1)
(clear b3)
(clear b4)
(clear b6)
(clear b8)
)
(:goal
(and
(on b3 b7)
(on b4 b8)
(on b6 b2)
(on b7 b4)
(on b8 b5)
(on b9 b1))
)
)


