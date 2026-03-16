

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b3)
(on b2 b1)
(on b3 b4)
(on b4 b7)
(on b5 b6)
(on b6 b8)
(ontable b7)
(ontable b8)
(clear b2)
(clear b5)
)
(:goal
(and
(on b1 b5)
(on b2 b4)
(on b3 b6)
(on b4 b3)
(on b6 b8)
(on b8 b1))
)
)


