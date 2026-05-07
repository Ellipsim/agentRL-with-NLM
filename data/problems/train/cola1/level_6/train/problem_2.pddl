

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(ontable b1)
(on b2 b3)
(on b3 b6)
(on b4 b8)
(on b5 b2)
(on b6 b4)
(ontable b7)
(ontable b8)
(clear b1)
(clear b5)
(clear b7)
)
(:goal
(and
(on b2 b1)
(on b3 b5)
(on b4 b6)
(on b5 b7)
(on b7 b4)
(on b8 b2))
)
)


