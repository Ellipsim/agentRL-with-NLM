

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(on b1 b8)
(on b2 b9)
(ontable b3)
(on b4 b7)
(on b5 b3)
(on b6 b4)
(on b7 b1)
(ontable b8)
(ontable b9)
(clear b2)
(clear b5)
(clear b6)
)
(:goal
(and
(on b2 b9)
(on b3 b8)
(on b6 b4)
(on b7 b3)
(on b8 b5))
)
)


