

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(on b1 b5)
(ontable b2)
(on b3 b7)
(ontable b4)
(on b5 b4)
(on b6 b1)
(on b7 b9)
(on b8 b2)
(ontable b9)
(clear b3)
(clear b6)
(clear b8)
)
(:goal
(and
(on b1 b2)
(on b3 b6)
(on b4 b7)
(on b5 b3)
(on b6 b9)
(on b7 b8)
(on b8 b5))
)
)


