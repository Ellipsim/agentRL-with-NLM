

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b6)
(on b2 b1)
(on b3 b5)
(ontable b4)
(ontable b5)
(on b6 b9)
(on b7 b2)
(ontable b8)
(on b9 b10)
(on b10 b4)
(clear b3)
(clear b7)
(clear b8)
)
(:goal
(and
(on b2 b8)
(on b3 b5)
(on b4 b3)
(on b5 b9)
(on b6 b4)
(on b9 b1)
(on b10 b7))
)
)


