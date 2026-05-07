

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(ontable b1)
(on b2 b6)
(on b3 b4)
(ontable b4)
(ontable b5)
(on b6 b1)
(on b7 b5)
(ontable b8)
(clear b2)
(clear b3)
(clear b7)
(clear b8)
)
(:goal
(and
(on b1 b6)
(on b4 b1)
(on b5 b8)
(on b6 b7)
(on b7 b5)
(on b8 b2))
)
)


