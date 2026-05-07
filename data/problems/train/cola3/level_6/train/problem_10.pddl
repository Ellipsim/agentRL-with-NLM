

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b2)
(on b2 b8)
(ontable b3)
(ontable b4)
(on b5 b4)
(on b6 b5)
(on b7 b3)
(ontable b8)
(clear b1)
(clear b6)
(clear b7)
)
(:goal
(and
(on b3 b8)
(on b4 b2)
(on b5 b7)
(on b7 b3)
(on b8 b1))
)
)


