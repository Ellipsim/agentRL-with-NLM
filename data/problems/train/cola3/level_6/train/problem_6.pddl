

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b3)
(on b2 b7)
(ontable b3)
(ontable b4)
(ontable b5)
(ontable b6)
(on b7 b5)
(on b8 b4)
(clear b1)
(clear b2)
(clear b6)
(clear b8)
)
(:goal
(and
(on b1 b5)
(on b2 b8)
(on b3 b7)
(on b5 b4)
(on b6 b1)
(on b8 b6))
)
)


