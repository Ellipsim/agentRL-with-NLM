

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b3)
(on b2 b1)
(on b3 b7)
(ontable b4)
(on b5 b6)
(on b6 b12)
(on b7 b4)
(on b8 b11)
(on b9 b8)
(on b10 b5)
(ontable b11)
(ontable b12)
(clear b2)
(clear b9)
(clear b10)
)
(:goal
(and
(on b2 b3)
(on b3 b11)
(on b5 b6)
(on b6 b9)
(on b8 b4)
(on b9 b2)
(on b10 b1)
(on b11 b10)
(on b12 b8))
)
)


