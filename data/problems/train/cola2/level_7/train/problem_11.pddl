

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(ontable b1)
(on b2 b1)
(on b3 b5)
(ontable b4)
(ontable b5)
(on b6 b2)
(on b7 b4)
(on b8 b9)
(on b9 b7)
(clear b3)
(clear b6)
(clear b8)
)
(:goal
(and
(on b2 b7)
(on b3 b2)
(on b5 b6)
(on b6 b8)
(on b8 b4)
(on b9 b5))
)
)


