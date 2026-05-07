

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(ontable b1)
(on b2 b3)
(on b3 b8)
(on b4 b6)
(ontable b5)
(on b6 b9)
(ontable b7)
(ontable b8)
(on b9 b7)
(clear b1)
(clear b2)
(clear b4)
(clear b5)
)
(:goal
(and
(on b2 b5)
(on b3 b1)
(on b4 b8)
(on b6 b7)
(on b7 b3)
(on b9 b4))
)
)


